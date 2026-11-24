// Copy the page this program ships beside itself, entry.png, to the directory
// the grader reads. Node 22, standard library only: no clock, no network, no
// environment but the output directory, so two runs write the same bytes.
//
// Why the program reads the PNG header itself instead of trusting the file: the
// gate only takes a whole PNG or JPEG, so a truncated download, an empty
// placeholder or a JPEG saved under a .png name passes a plain copy and fails at
// the gate, after the run, with no chance left to fix it. Checking the first
// eight bytes here turns that into a message naming the file and the reason
// while it can still be acted on. A name ending in .png is a claim by whoever
// wrote the file; the signature is part of the image data itself.

import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const LIMIT_BYTES = 1048576;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// A named error, so a failed run says which rule it broke rather than "ENOENT".
class EntryError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'EntryError';
  }
}

// The page sits beside this module, wherever the repository is mounted.
const pagePath = fileURLToPath(new URL('./entry.png', import.meta.url));

let pageBytes: Buffer;
try {
  if (!statSync(pagePath).isFile()) throw new EntryError(`entry.png is not a regular file: ${pagePath}`);
  pageBytes = readFileSync(pagePath);
} catch (cause) {
  if (cause instanceof EntryError) throw cause;
  throw new EntryError(`entry.png is missing or unreadable at ${pagePath}: ${(cause as Error).message}`);
}

if (pageBytes.length > LIMIT_BYTES) {
  throw new EntryError(`entry.png is ${pageBytes.length} bytes, above the ${LIMIT_BYTES}-byte limit`);
}

if (pageBytes.length < PNG_SIGNATURE.length || !pageBytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new EntryError(
    `entry.png does not start with the 8-byte PNG signature, found ${pageBytes.subarray(0, 8).toString('hex')}`,
  );
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });

const destination = join(outputDir, 'entry.png');
copyFileSync(pagePath, destination);

// copyFileSync proves nothing, so size the copy: a short write, a stale file
// left at the destination or a quiet truncation would ship unlooked-at bytes.
const copiedBytes = statSync(destination).size;
if (copiedBytes !== pageBytes.length) {
  throw new EntryError(
    `copied ${destination} is ${copiedBytes} bytes but ${pageBytes.length} bytes were read from ${pagePath}`,
  );
}

const digest = createHash('sha256').update(pageBytes).digest('hex');
console.log(`wrote ${destination} (${copiedBytes} bytes, PNG signature checked, sha256 ${digest})`);
