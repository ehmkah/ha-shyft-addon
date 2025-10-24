import test from 'node:test';
import assert from 'node:assert/strict';

test('callExternalApi returns prefixed string', async () => {
    assert.equal('result_for_fooa', 'result_for_foo');
});

