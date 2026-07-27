-- ViajApp: Tablas nuevas para FASE 3
-- Ejecutar en Supabase SQL Editor

-- 1. Tabla de valoraciones
CREATE TABLE IF NOT EXISTS reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  itinerary_id UUID NOT NULL REFERENCES itineraries(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(itinerary_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_reviews_itinerary ON reviews(itinerary_id);
CREATE INDEX IF NOT EXISTS idx_reviews_user ON reviews(user_id);

-- 2. Tabla de grupos de gastos
CREATE TABLE IF NOT EXISTS expense_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_expense_groups_user ON expense_groups(user_id);

-- 3. Tabla de miembros de grupo
CREATE TABLE IF NOT EXISTS expense_group_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  group_id UUID NOT NULL REFERENCES expense_groups(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_expense_group_members_group ON expense_group_members(group_id);

-- 4. Tabla de gastos
CREATE TABLE IF NOT EXISTS expenses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  group_id UUID NOT NULL REFERENCES expense_groups(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount DECIMAL(10,2) NOT NULL,
  currency TEXT DEFAULT 'JPY',
  description TEXT NOT NULL,
  paid_by TEXT DEFAULT '',
  split_with JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_expenses_group ON expenses(group_id);

-- 5. Tabla de consejos de la comunidad
CREATE TABLE IF NOT EXISTS community_tips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  category TEXT DEFAULT 'general',
  city TEXT DEFAULT '',
  tags TEXT DEFAULT '',
  approved BOOLEAN DEFAULT TRUE,
  likes INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_community_tips_category ON community_tips(category);
CREATE INDEX IF NOT EXISTS idx_community_tips_approved ON community_tips(approved);

-- 6. Añadir is_shared a itineraries si no existe
ALTER TABLE itineraries ADD COLUMN IF NOT EXISTS is_shared BOOLEAN DEFAULT FALSE;

-- 7. RLS (Row Level Security) — desactivar para desarrollo, activar en produccion
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE expense_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE expense_group_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_tips ENABLE ROW LEVEL SECURITY;

-- Politicas para reviews
CREATE POLICY "Users can view all reviews" ON reviews FOR SELECT USING (true);
CREATE POLICY "Users can create reviews" ON reviews FOR INSERT WITH CHECK (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));
CREATE POLICY "Users can delete own reviews" ON reviews FOR DELETE USING (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));

-- Politicas para expense_groups
CREATE POLICY "Users can view own groups" ON expense_groups FOR SELECT USING (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));
CREATE POLICY "Users can create groups" ON expense_groups FOR INSERT WITH CHECK (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));
CREATE POLICY "Users can delete own groups" ON expense_groups FOR DELETE USING (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));

-- Politicas para expense_group_members
CREATE POLICY "Users can view group members" ON expense_group_members FOR SELECT USING (true);
CREATE POLICY "Users can add members" ON expense_group_members FOR INSERT WITH CHECK (true);

-- Politicas para expenses
CREATE POLICY "Users can view group expenses" ON expenses FOR SELECT USING (true);
CREATE POLICY "Users can create expenses" ON expenses FOR INSERT WITH CHECK (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));
CREATE POLICY "Users can delete own expenses" ON expenses FOR DELETE USING (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));

-- Politicas para community_tips
CREATE POLICY "Anyone can view approved tips" ON community_tips FOR SELECT USING (approved = true);
CREATE POLICY "Users can create tips" ON community_tips FOR INSERT WITH CHECK (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));
CREATE POLICY "Users can like tips" ON community_tips FOR UPDATE USING (true);
CREATE POLICY "Users can delete own tips" ON community_tips FOR DELETE USING (auth.uid()::text = (SELECT id::text FROM users WHERE id = user_id));
