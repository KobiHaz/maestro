#!/usr/bin/env node
/**
 * Creates "Consul House - Leads" Google Sheet with Registry and Audit Log tabs.
 * Requires: GOOGLE_APPLICATION_CREDENTIALS env var or --credentials path
 * Run: node create-consul-house-sheet.mjs
 */

import { google } from 'googleapis';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const CREDENTIALS_PATH = process.env.GOOGLE_APPLICATION_CREDENTIALS 
  || join(process.env.HOME || '', '.google/consul-house-sheets.json');

const SCOPES = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive.file',
];

async function main() {
  let auth;
  try {
    const keyFile = readFileSync(CREDENTIALS_PATH, 'utf8');
    const key = JSON.parse(keyFile);
    auth = new google.auth.GoogleAuth({
      credentials: key,
      scopes: SCOPES,
    });
    console.log('📁 Using Service Account from:', CREDENTIALS_PATH);
  } catch {
    console.log('📁 No credentials file — trying Application Default Credentials (gcloud)...');
    auth = new google.auth.GoogleAuth({
      scopes: SCOPES,
    });
  }

  const sheets = google.sheets({ version: 'v4', auth });

  const requestBody = {
    properties: { title: 'Consul House - Leads' },
    sheets: [
      {
        properties: { title: 'Registry' },
        data: [{
          startRow: 0,
          rowData: [{
            values: [
              { userEnteredValue: { stringValue: 'First Name' } },
              { userEnteredValue: { stringValue: 'Last Name' } },
              { userEnteredValue: { stringValue: 'Phone' } },
              { userEnteredValue: { stringValue: 'Email' } },
              { userEnteredValue: { stringValue: 'Event Type' } },
              { userEnteredValue: { stringValue: 'Guests' } },
              { userEnteredValue: { stringValue: 'Notes' } },
              { userEnteredValue: { stringValue: 'Created At' } },
              { userEnteredValue: { stringValue: 'Status' } },
              { userEnteredValue: { stringValue: 'Retry' } },
              { userEnteredValue: { stringValue: 'Updated At' } },
              { userEnteredValue: { stringValue: 'Source' } },
              { userEnteredValue: { stringValue: 'iPlan Lead Id' } },
            ],
          }],
        }],
      },
      {
        properties: { title: 'Audit Log' },
        data: [{
          startRow: 0,
          rowData: [{
            values: [
              { userEnteredValue: { stringValue: 'timestamp' } },
              { userEnteredValue: { stringValue: 'run_id' } },
              { userEnteredValue: { stringValue: 'email' } },
              { userEnteredValue: { stringValue: 'phone' } },
              { userEnteredValue: { stringValue: 'source' } },
              { userEnteredValue: { stringValue: 'decision' } },
              { userEnteredValue: { stringValue: 'reason' } },
              { userEnteredValue: { stringValue: 'metadata' } },
            ],
          }],
        }],
      },
    ],
  };

  try {
    const res = await sheets.spreadsheets.create({ requestBody });
    const id = res.data.spreadsheetId;
    const url = `https://docs.google.com/spreadsheets/d/${id}/edit`;
    console.log('✅ Created: Consul House - Leads');
    console.log('   URL:', url);
    console.log('   ID:', id);
    console.log('\n⚠️  Share this sheet with your Make connection (or service account email) for automation.');
  } catch (err) {
    console.error('❌ API Error:', err.message);
    if (err.message?.includes('403')) {
      console.error('   Enable Google Sheets API: https://console.cloud.google.com/apis/library/sheets.googleapis.com');
    }
    process.exit(1);
  }
}

main();
