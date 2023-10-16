import URI from "urijs";

import { parseReportData } from "./parseReportData";

/**
 * An individual dialect of JSON Schema.
 */
export default class Dialect {
  readonly path: string;
  readonly prettyName: string;
  readonly uri: string;

  private static all: Map<string, Dialect> = new Map<string, Dialect>();

  constructor(path: string, prettyName: string, uri: string) {
    if (Dialect.all.has(path)) {
      throw new DialectError(`A "${path}" dialect already exists.`);
    }
    Dialect.all.set(path, this);

    this.path = path;
    this.prettyName = prettyName;
    this.uri = uri;
  }

  async fetchReport(baseURI: URI) {
    const url = baseURI.clone().filename(this.path).suffix("json").href();
    const response = await fetch(url);
    const jsonl = await response.text();
    const lines = jsonl
      .trim()
      .split(/\r?\n/)
      .map((line) => JSON.parse(line));
    return parseReportData(lines);
  }

  static known(): Iterable<Dialect> {
    return Dialect.all.values();
  }

  static forPath(path: string): Dialect {
    const dialect = Dialect.all.get(path);
    if (!dialect) {
      throw new DialectError(`A ${path} dialect does not exist.`);
    }
    return dialect;
  }
}

class DialectError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DialectError";
    Object.setPrototypeOf(this, DialectError.prototype);
  }
}

export const DRAFT202012 = new Dialect(
  "draft2020-12",
  "Draft 2020-12",
  "https://json-schema.org/draft/2020-12/schema",
);
export const DRAFT201909 = new Dialect(
  "draft2019-09",
  "Draft 2019-09",
  "https://json-schema.org/draft/2019-09/schema",
);
export const DRAFT7 = new Dialect(
  "draft7",
  "Draft 7",
  "http://json-schema.org/draft-07/schema#",
);
export const DRAFT6 = new Dialect(
  "draft6",
  "Draft 6",
  "http://json-schema.org/draft-06/schema#",
);
export const DRAFT4 = new Dialect(
  "draft4",
  "Draft 4",
  "http://json-schema.org/draft-04/schema#",
);
export const DRAFT3 = new Dialect(
  "draft3",
  "Draft 3",
  "http://json-schema.org/draft-03/schema#",
);
