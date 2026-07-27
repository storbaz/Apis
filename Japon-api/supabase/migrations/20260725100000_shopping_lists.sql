-- Shopping lists table
CREATE TABLE IF NOT EXISTS shopping_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    trip_id UUID,
    share_token VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Shopping items table
CREATE TABLE IF NOT EXISTS shopping_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    list_id UUID NOT NULL REFERENCES shopping_lists(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    store VARCHAR(100) DEFAULT '',
    quantity INT DEFAULT 1,
    checked BOOLEAN DEFAULT false,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_shopping_lists_user_id ON shopping_lists(user_id);
CREATE INDEX IF NOT EXISTS idx_shopping_lists_share_token ON shopping_lists(share_token);
CREATE INDEX IF NOT EXISTS idx_shopping_items_list_id ON shopping_items(list_id);

-- RLS policies
ALTER TABLE shopping_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE shopping_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own shopping lists" ON shopping_lists
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE email = auth.email()));

CREATE POLICY "Users can insert own shopping lists" ON shopping_lists
    FOR INSERT WITH CHECK (user_id IN (SELECT id FROM users WHERE email = auth.email()));

CREATE POLICY "Users can delete own shopping lists" ON shopping_lists
    FOR DELETE USING (user_id IN (SELECT id FROM users WHERE email = auth.email()));

-- Public read for shared lists (by share_token)
CREATE POLICY "Anyone can view shared shopping lists" ON shopping_lists
    FOR SELECT USING (true);

CREATE POLICY "Users can view own shopping items" ON shopping_items
    FOR SELECT USING (list_id IN (SELECT id FROM shopping_lists WHERE user_id IN (SELECT id FROM users WHERE email = auth.email())));

CREATE POLICY "Users can insert own shopping items" ON shopping_items
    FOR INSERT WITH CHECK (list_id IN (SELECT id FROM shopping_lists WHERE user_id IN (SELECT id FROM users WHERE email = auth.email())));

CREATE POLICY "Users can delete own shopping items" ON shopping_items
    FOR DELETE USING (list_id IN (SELECT id FROM shopping_lists WHERE user_id IN (SELECT id FROM users WHERE email = auth.email())));
