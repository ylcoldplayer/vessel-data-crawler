import { Config } from "./config.js";
import { Page } from "playwright";
export declare function getPageHtml(page: Page, selector?: string): Promise<string>;
export declare function waitForXPath(page: Page, xpath: string, timeout: number): Promise<void>;
export declare function crawl(config: Config): Promise<void>;
export declare function write(config: Config): Promise<void>;
//# sourceMappingURL=core.d.ts.map