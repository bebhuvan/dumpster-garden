import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
 configuration: {
   pageTitle: "🗑️🔥From the dumpster fire ",
   pageTitleSuffix: "",
   enableSPA: true,
   enablePopovers: true,
   analytics: {
     provider: "plausible",
   },
   description: "A personal digital garden where I share interesting finds from around the web and my own thoughts.",
   defaultLanguage: 'en',
   locale: "en-US",
   baseUrl: "fromthedumpsterfire.com",
   ignorePatterns: ["private", "templates", ".obsidian"],
   defaultDateType: "created",
   generateSocialImages: false,
   displayHeader: false,
   footer: {
     links: [
       { path: "https://x.com/bebhuvan", text: "Twitter" },
       { path: "https://www.linkedin.com/in/bebhuvan/", text: "LinkedIn" }
     ]
   },
   theme: {
     fontOrigin: "googleFonts",
     cdnCaching: true,
     typography: {
       header: "Schibsted Grotesk",
       body: "Source Sans Pro",
       code: "IBM Plex Mono",
     },
     colors: {
       lightMode: {
         light: "#ffffff",      // Pure white background
         lightgray: "#E6DCCC",  // Warm gray
         gray: "#93836C",       // Dusty brown
         darkgray: "#544B3D",   // Dark earthy tone
         dark: "#2C2824",       // Almost black with warmth
         secondary: "#FF6B35",  // Warm orange (fire)
         tertiary: "#666666",   // Industrial gray
         highlight: "rgba(255, 107, 53, 0.15)", // Light orange highlight
         textHighlight: "#FFE1D566", // Warm highlight
       },
       darkMode: {
         light: "#232020",      // Dark warm background
         lightgray: "#423D3D",  // Dark warm gray
         gray: "#767676",       // Industrial metal gray
         darkgray: "#B4A89D",   // Warm light gray
         dark: "#E8E3DD",       // Warm white
         secondary: "#FF914D",  // Bright orange (fire)
         tertiary: "#9C9C9C",   // Steel gray
         highlight: "rgba(255, 145, 77, 0.15)", // Dark orange highlight
         textHighlight: "#FFB86C44", // Warm highlight
       },
     },
   },
 },
 plugins: {
   transformers: [
     Plugin.FrontMatter(),
     Plugin.CreatedModifiedDate({
       priority: ["frontmatter", "filesystem"],
     }),
     Plugin.SyntaxHighlighting({
       theme: {
         light: "github-light",
         dark: "github-dark",
       },
       keepBackground: false,
     }),
     Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
     Plugin.GitHubFlavoredMarkdown(),
     Plugin.TableOfContents(),
     Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
     Plugin.Description(),
     Plugin.Latex({ renderEngine: "katex" })  
   ],
   filters: [Plugin.RemoveDrafts()],
   emitters: [
     Plugin.AliasRedirects(),
     Plugin.ComponentResources(),
     Plugin.ContentPage({
       pageLayout: {
         showDate: false,
         showDescription: false,
         showReadingTime: false
       }
     }),
     Plugin.FolderPage(),
     Plugin.TagPage(),
     Plugin.ContentIndex({
       enableSiteMap: true,
       enableRSS: true,
     }),
     Plugin.Assets(),
     Plugin.Static(),
     Plugin.NotFoundPage()
   ]
 }
}

export default config
