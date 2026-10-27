import http from 'k6/http';
import { check, sleep, group } from 'k6';

// Thresholds configuration
export const options = {
  stages: [
    { duration: '10s', target: 5 },   // Ramp-up to  five VUs
    { duration: '30s', target: 5 },   // Run with 5 VUs
    { duration: '10s', target: 0 },   // Ramp-down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<300'], // 95% of requests under 300 ms
    'http_req_failed': ['rate<0.01'],   // Error rate must be less than 1 %
  },
};

// URL runs on localhost by default, can be overridden with the BASE_URL environment variable
const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8000';

export default function () {
  let itemId;

  group('E2E CRUD Workflow', function () {
    
    // 1. CREATE Item
    const createPayload = JSON.stringify({
      name: `Karta k6 - VU ${__VU} Iter ${__ITER}`,
      description: 'E2E K6 test item',
      price: 150.50 + __VU,
    });
    const params = {
      headers: { 'Content-Type': 'application/json' },
    };

    let res = http.post(`${BASE_URL}/items/`, createPayload, params);
    let success = check(res, {
      'POST /items/ status equal 201': (r) => r.status === 201,
      'POST /items/ returns ID': (r) => r.json('id') !== undefined,
    });

    if (!success || res.status !== 201) {
      return; // can not create item, skip the rest of the test for this iteration
    }
    itemId = res.json('id');

    // 2. READ ALL items
    res = http.get(`${BASE_URL}/items/`);
    check(res, {
      'GET /items/ status is 200': (r) => r.status === 200,
      'GET /items/ contains data': (r) => r.json().length > 0,
    });

    // 3. READ ONE item
    res = http.get(`${BASE_URL}/items/${itemId}`);
    check(res, {
      'GET /items/{id} status is 200': (r) => r.status === 200,
      'ID matches created item': (r) => r.json('id') === itemId,
    });

    // 4. UPDATE Item
    const updatePayload = JSON.stringify({
      price: 299.99,
    });
    res = http.put(`${BASE_URL}/items/${itemId}`, updatePayload, params);
    check(res, {
      'PUT /items/{id} status is 200': (r) => r.status === 200,
      'Price was updated': (r) => r.json('price') === 299.99,
    });

    // 5. DELETE Item
    res = http.del(`${BASE_URL}/items/${itemId}`);
    check(res, {
      'DELETE /items/{id} status is 204': (r) => r.status === 204,
    });

    // 6. VERIFY DELETE: 
    res = http.get(`${BASE_URL}/items/${itemId}`);
    check(res, {
      'GET deleted item returns 404': (r) => r.status === 404,
    });
  });

  // Sleep for a second between iterations
  sleep(1);
}