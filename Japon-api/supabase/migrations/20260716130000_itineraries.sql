-- Itineraries table
CREATE TABLE IF NOT EXISTS itineraries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Itinerary items table
CREATE TABLE IF NOT EXISTS itinerary_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    itinerary_id UUID NOT NULL REFERENCES itineraries(id) ON DELETE CASCADE,
    day_number INT NOT NULL,
    time VARCHAR(10) DEFAULT '',
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    location VARCHAR(255) DEFAULT '',
    category VARCHAR(50) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_itineraries_user_id ON itineraries(user_id);
CREATE INDEX IF NOT EXISTS idx_itinerary_items_itinerary_id ON itinerary_items(itinerary_id);

-- RLS policies
ALTER TABLE itineraries ENABLE ROW LEVEL SECURITY;
ALTER TABLE itinerary_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own itineraries" ON itineraries
    FOR SELECT USING (user_id IN (SELECT id FROM users WHERE email = auth.email()));

CREATE POLICY "Users can insert own itineraries" ON itineraries
    FOR INSERT WITH CHECK (user_id IN (SELECT id FROM users WHERE email = auth.email()));

CREATE POLICY "Users can update own itineraries" ON itineraries
    FOR UPDATE USING (user_id IN (SELECT id FROM users WHERE email = auth.email()));

CREATE POLICY "Users can delete own itineraries" ON itineraries
    FOR DELETE USING (user_id IN (SELECT id FROM users WHERE email = auth.email()));

CREATE POLICY "Users can view own itinerary items" ON itinerary_items
    FOR SELECT USING (itinerary_id IN (SELECT id FROM itineraries WHERE user_id IN (SELECT id FROM users WHERE email = auth.email())));

CREATE POLICY "Users can insert own itinerary items" ON itinerary_items
    FOR INSERT WITH CHECK (itinerary_id IN (SELECT id FROM itineraries WHERE user_id IN (SELECT id FROM users WHERE email = auth.email())));

CREATE POLICY "Users can delete own itinerary items" ON itinerary_items
    FOR DELETE USING (itinerary_id IN (SELECT id FROM itineraries WHERE user_id IN (SELECT id FROM users WHERE email = auth.email())));
