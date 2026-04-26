-- ============================================
-- Fred Baker's Automations
-- Nigeria Business Database — Saved Queries
-- ============================================

-- 1. All LexAI prospects
SELECT company_name, city, sector, prospect_for
FROM businesses
WHERE prospect_for = 'LexAI'
ORDER BY city;

-- 2. Count by product
SELECT prospect_for, COUNT(*) as total
FROM businesses
GROUP BY prospect_for
ORDER BY total DESC;

-- 3. All uncontacted businesses
SELECT company_name, city, prospect_for, status
FROM businesses
WHERE contacted = 0
ORDER BY city;

-- 4. Oil & Gas businesses
SELECT company_name, city, phone, website
FROM businesses
WHERE sector = 'Oil & Gas'
ORDER BY city;

-- 5. City breakdown pivot
SELECT 
    city,
    COUNT(*) as total_businesses,
    SUM(CASE WHEN prospect_for = 'LexAI' THEN 1 ELSE 0 END) as lexai,
    SUM(CASE WHEN prospect_for = 'EstateIQ' THEN 1 ELSE 0 END) as estateiq,
    SUM(CASE WHEN prospect_for = 'OpsGuard' THEN 1 ELSE 0 END) as opsguard
FROM businesses
GROUP BY city
ORDER BY total_businesses DESC;

-- 6. Priority outreach ranking
SELECT 
    company_name,
    city,
    prospect_for,
    CASE 
        WHEN city = 'Lagos' AND prospect_for = 'LexAI' THEN 'Priority 1'
        WHEN city = 'Abuja' AND prospect_for = 'LexAI' THEN 'Priority 2'
        WHEN prospect_for = 'OpsGuard' THEN 'Priority 3'
        ELSE 'Standard'
    END as outreach_priority
FROM businesses
WHERE contacted = 0
ORDER BY outreach_priority;