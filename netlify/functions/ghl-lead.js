// netlify/functions/ghl-lead.js
// Receives the "GET A FREE QUOTE" contact form submission from the website and
// creates/updates the lead in GoHighLevel via the Private Integration API.
//
// The GHL Private Integration token is read from the GHL_PIT_TOKEN environment
// variable (set in Netlify > Site settings > Environment variables). It is never
// placed in client-side code or committed to the repo, so it stays private.

const GHL_UPSERT_URL = 'https://services.leadconnectorhq.com/contacts/upsert';
const LOCATION_ID = 'ivspLzujgp6sa9yA2MAn';       // Ramos Roofing GHL subaccount (not secret)
const MESSAGE_FIELD_ID = 'hHb52g9rwAuGfgZW6aFA';  // Contact custom field "Their Message" (contact.their_message)
const LEAD_TAG = 'website form lead';             // Triggers the "Website Form Notification" automation

// Normalize US numbers to E.164 so GHL can reliably send the SMS auto-reply.
function normalizePhone(raw) {
  const digits = (raw || '').replace(/\D/g, '');
  if (digits.length === 10) return '+1' + digits;
  if (digits.length === 11 && digits.startsWith('1')) return '+' + digits;
  return raw; // leave anything unexpected as entered
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  const token = process.env.GHL_PIT_TOKEN;
  if (!token) {
    console.error('GHL_PIT_TOKEN environment variable is not set.');
    return { statusCode: 500, body: JSON.stringify({ error: 'Server not configured' }) };
  }

  let data;
  try {
    data = JSON.parse(event.body || '{}');
  } catch (err) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid request' }) };
  }

  // Honeypot: real users never see the "company" field. If it's filled, it's a
  // bot — pretend everything worked and drop it.
  if (data.company) {
    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  }

  const name = (data.name || '').trim();
  const phone = (data.phone || '').trim();
  const email = (data.email || '').trim();
  const message = (data.message || '').trim();

  if (!name || !phone) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Name and phone are required.' }) };
  }

  const payload = {
    locationId: LOCATION_ID,
    name: name,
    phone: normalizePhone(phone),
    source: 'Website Quote Form',
    tags: [LEAD_TAG],
  };
  if (email) payload.email = email;
  if (message) payload.customFields = [{ id: MESSAGE_FIELD_ID, value: message }];

  try {
    const res = await fetch(GHL_UPSERT_URL, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        Version: '2021-07-28',
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const result = await res.json().catch(() => ({}));

    if (!res.ok) {
      console.error('GHL upsert failed:', res.status, result);
      return { statusCode: 502, body: JSON.stringify({ error: 'Could not submit your request. Please call us.' }) };
    }

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    console.error('GHL request error:', err);
    return { statusCode: 502, body: JSON.stringify({ error: 'Could not submit your request. Please call us.' }) };
  }
};
