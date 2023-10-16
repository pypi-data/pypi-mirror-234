export default {
  "title": "Soil SDK",
  "tagline": "Soil's Software Development Kit",
  "url": "https://developer.amalfianalytics.com",
  "baseUrl": "/",
  "organizationName": "Amalfi Analytics",
  "projectName": "soil-sdk",
  "scripts": [
    "https://buttons.github.io/buttons.js"
  ],
  "favicon": "img/favicon_amalfi.png",
  "customFields": {
    "users": [
      {
        "caption": "User1",
        "image": "/img/undraw_open_source.svg",
        "infoLink": "https://www.facebook.com",
        "pinned": true
      }
    ],
    "repoUrl": "https://gitlab.com/amalfianalytics/soil/soil-sdk"
  },
  "onBrokenLinks": "log",
  "onBrokenMarkdownLinks": "log",
  "presets": [
    [
      "@docusaurus/preset-classic",
      {
        "docs": {
          "showLastUpdateAuthor": true,
          "showLastUpdateTime": true,
          "editUrl": "https://gitlab.com/amalfianalytics/soil/soil-sdk/-/tree/master/docs/docs/",
          "path": "../docs",
          "sidebarPath": "./sidebars.js"
        },
        "blog": {
          "path": "blog"
        },
        "theme": {
          "customCss": "../src/css/customTheme.css"
        }
      }
    ]
  ],
  "plugins": [],
  "themeConfig": {
    "navbar": {
      "title": "Soil SDK",
      "logo": {
        "src": "img/favicon_amalfi.png"
      },
      "items": [
        {
          "to": "docs/tutorial/get-started",
          "label": "Tutorial",
          "position": "left"
        },
        {
          "to": "docs/soil-library/modules/experiment",
          "label": "Soil Library",
          "position": "left"
        },
        {
          "to": "docs/sdk-reference/soil/data",
          "label": "SDK Reference",
          "position": "left"
        }
      ],
      "hideOnScroll": false
    },
    "image": "img/undraw_online.svg",
    "footer": {
      "links": [],
      "copyright": "Copyright © 2021 Amalfi Analytics",
      "logo": {
        "src": "img/favicon_amalfi.png"
      },
      "style": "light"
    },
    "colorMode": {
      "defaultMode": "light",
      "disableSwitch": false,
      "respectPrefersColorScheme": false,
      "switchConfig": {
        "darkIcon": "🌜",
        "darkIconStyle": {},
        "lightIcon": "🌞",
        "lightIconStyle": {}
      }
    },
    "docs": {
      "versionPersistence": "localStorage"
    },
    "metadatas": [],
    "prism": {
      "additionalLanguages": []
    },
    "hideableSidebar": false
  },
  "baseUrlIssueBanner": true,
  "i18n": {
    "defaultLocale": "en",
    "locales": [
      "en"
    ],
    "localeConfigs": {}
  },
  "onDuplicateRoutes": "warn",
  "themes": [],
  "titleDelimiter": "|",
  "noIndex": false
};