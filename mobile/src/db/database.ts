import * as SQLite from "expo-sqlite";
export const db=SQLite.openDatabaseSync("fraud_inspection.db");
export function initializeDatabase(){db.execSync(`CREATE TABLE IF NOT EXISTS missions(id TEXT PRIMARY KEY,customer_id TEXT NOT NULL,customer_name TEXT,latitude REAL,longitude REAL,risk_score REAL,status TEXT,updated_at TEXT,sync_status TEXT DEFAULT 'SYNCED');CREATE TABLE IF NOT EXISTS inspection_queue(id TEXT PRIMARY KEY,payload TEXT NOT NULL,created_at TEXT NOT NULL,retry_count INTEGER DEFAULT 0);`)}
export function queueInspection(id:string,payload:unknown){db.runSync("INSERT OR REPLACE INTO inspection_queue(id,payload,created_at) VALUES(?,?,?)",[id,JSON.stringify(payload),new Date().toISOString()])}
