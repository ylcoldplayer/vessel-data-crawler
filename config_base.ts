import { Config } from "./src/config";

export const defaultConfig: Config = {
  url: "https://www.balticexchange.com/en/index.html",
  match: "https://www.balticexchange.com/en/index.html",
  maxPagesToCrawl: 50,
  outputFileName: "output.json",
};