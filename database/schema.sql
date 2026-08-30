CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 username VARCHAR(100) UNIQUE NOT NULL,
 email VARCHAR(255) UNIQUE NOT NULL,
 password_hash TEXT NOT NULL,
 role VARCHAR(50) NOT NULL DEFAULT 'AGENT',
 is_active BOOLEAN DEFAULT TRUE,
 created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customers (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 external_id VARCHAR(100) UNIQUE,
 account_number VARCHAR(100) UNIQUE NOT NULL,
 full_name VARCHAR(255),
 phone VARCHAR(50),
 address TEXT,
 voltage VARCHAR(10) NOT NULL DEFAULT 'BT',
 phase VARCHAR(20) NOT NULL DEFAULT 'MONOPHASE',
 subscribed_power_kw NUMERIC(12,2),
 geom GEOGRAPHY(POINT,4326),
 updated_at TIMESTAMPTZ DEFAULT NOW(),
 created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_customers_geom ON customers USING GIST(geom);

CREATE TABLE IF NOT EXISTS meters (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
 meter_number VARCHAR(100) UNIQUE NOT NULL,
 meter_type VARCHAR(50),
 status VARCHAR(30) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS meter_readings (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 meter_id UUID REFERENCES meters(id) ON DELETE CASCADE,
 reading_time TIMESTAMPTZ NOT NULL,
 active_energy_kwh NUMERIC(18,4),
 reactive_energy_kvarh NUMERIC(18,4),
 voltage NUMERIC(10,2),
 current NUMERIC(10,2),
 load_profile JSONB,
 source VARCHAR(50),
 created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_meter_readings_meter_time ON meter_readings(meter_id, reading_time DESC);

CREATE TABLE IF NOT EXISTS fraud_scores (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
 risk_score NUMERIC(5,2) CHECK (risk_score BETWEEN 0 AND 100),
 estimated_loss_kwh NUMERIC(18,2),
 estimated_loss_amount NUMERIC(18,2),
 anomaly_ratio NUMERIC(12,4),
 peer_deviation NUMERIC(12,4),
 model_version VARCHAR(100),
 explanation JSONB DEFAULT '{}'::jsonb,
 calculated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inspections (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 customer_id UUID REFERENCES customers(id),
 agent_id UUID REFERENCES users(id),
 status VARCHAR(30) DEFAULT 'PENDING',
 scheduled_at TIMESTAMPTZ,
 completed_at TIMESTAMPTZ,
 fraud_confirmed BOOLEAN,
 fraud_type VARCHAR(50),
 notes TEXT,
 inspection_geom GEOGRAPHY(POINT,4326),
 device_id VARCHAR(255),
 sync_version BIGINT DEFAULT 1,
 created_at TIMESTAMPTZ DEFAULT NOW(),
 updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inspection_evidence (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 inspection_id UUID REFERENCES inspections(id) ON DELETE CASCADE,
 evidence_type VARCHAR(30),
 file_url TEXT,
 sha256 VARCHAR(64),
 metadata JSONB DEFAULT '{}'::jsonb,
 created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID REFERENCES users(id),
 action VARCHAR(100) NOT NULL,
 entity_type VARCHAR(100),
 entity_id UUID,
 payload JSONB DEFAULT '{}'::jsonb,
 created_at TIMESTAMPTZ DEFAULT NOW()
);
