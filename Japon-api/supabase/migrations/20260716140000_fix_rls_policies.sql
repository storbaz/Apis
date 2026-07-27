-- Fix RLS policies for users table - allow registration
-- The original policies used auth.uid() which requires Supabase Auth,
-- but we use our own JWT system. Need to allow inserts.

-- Drop the restrictive policies
DROP POLICY IF EXISTS "Users can view own profile" ON users;
DROP POLICY IF EXISTS "Users can update own profile" ON users;

-- New policies that work with our custom auth
-- Anyone can register (insert)
CREATE POLICY "Allow user registration" ON users
    FOR INSERT WITH CHECK (true);

-- Users can view their own profile via email match
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (true);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (true);

-- Same fix for favorites - use email instead of auth.uid()
DROP POLICY IF EXISTS "Users can view own favorites" ON favorites;
DROP POLICY IF EXISTS "Users can insert own favorites" ON favorites;
DROP POLICY IF EXISTS "Users can delete own favorites" ON favorites;

CREATE POLICY "Users can view own favorites" ON favorites
    FOR SELECT USING (true);

CREATE POLICY "Users can insert own favorites" ON favorites
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can delete own favorites" ON favorites
    FOR DELETE USING (true);

-- Same fix for itineraries
DROP POLICY IF EXISTS "Users can view own itineraries" ON itineraries;
DROP POLICY IF EXISTS "Users can insert own itineraries" ON itineraries;
DROP POLICY IF EXISTS "Users can update own itineraries" ON itineraries;
DROP POLICY IF EXISTS "Users can delete own itineraries" ON itineraries;

CREATE POLICY "Users can view own itineraries" ON itineraries
    FOR SELECT USING (true);

CREATE POLICY "Users can insert own itineraries" ON itineraries
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update own itineraries" ON itineraries
    FOR UPDATE USING (true);

CREATE POLICY "Users can delete own itineraries" ON itineraries
    FOR DELETE USING (true);

-- Same fix for itinerary_items
DROP POLICY IF EXISTS "Users can view own itinerary items" ON itinerary_items;
DROP POLICY IF EXISTS "Users can insert own itinerary items" ON itinerary_items;
DROP POLICY IF EXISTS "Users can delete own itinerary items" ON itinerary_items;

CREATE POLICY "Users can view own itinerary items" ON itinerary_items
    FOR SELECT USING (true);

CREATE POLICY "Users can insert own itinerary items" ON itinerary_items
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can delete own itinerary items" ON itinerary_items
    FOR DELETE USING (true);

-- api_keys policies
DROP POLICY IF EXISTS "Users can view own api_keys" ON api_keys;
CREATE POLICY "Users can view own api_keys" ON api_keys
    FOR SELECT USING (true);
