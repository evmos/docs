// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/vsDark');

function defineSection(section, options = {}) {
  return [
    '@docusaurus/plugin-content-docs',
    /** @type {import('@docusaurus/plugin-content-docs').Options} */
    ({
      path: `docs/${section}`,
      routeBasePath: section,
      id: section,
      sidebarPath: require.resolve('./sidebars.js'),
      breadcrumbs: true,
      editUrl: 'https://github.com/evmos/docs/tree/main/',
      ...options,
    }),
  ];
}

const SECTIONS = [
  defineSection('use'),
  defineSection('develop'),
  defineSection('validate'),
  defineSection('protocol'),
  defineSection('api'),
];

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Evmos Docs',
  tagline: 'Develop on Evmos',
  url: 'https://docs.evmos.org',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'evmos', // Usually your GitHub org/user name.
  projectName: 'Docs', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  customFields: {
    project: {
      name: "Evmos",
      denom: "Evmos",
      ticker: "EVMOS",
      binary: "evmosd",
      testnet_denom: "tEvmos",
      testnet_ticker: "tEVMOS",
      rpc_url: "https://eth.bd.evmos.org:8545",
      rpc_url_testnet: "https://eth.bd.evmos.dev:8545",
      rpc_url_local: "http://localhost:8545/",
      chain_id: "9001",
      testnet_chain_id: "9000",
      latest_version: "v11.0.1",
      mainnet_version: "v11.0.1",
      testnet_version: "v11.0.1",
      version_number: "2",
      testnet_version_number: "4",
      testnet_evm_explorer_url: "https://evm.evmos.dev",
      evm_explorer_url: "https://escan.live",
      testnet_cosmos_explorer_url: "https://testnet.mintscan.io/evmos-testnet",
      cosmos_explorer_url: "https://www.mintscan.io/evmos",
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: 'docs/home',
          // routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          breadcrumbs: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
        gtag: {
          trackingID: 'G-3JSJBBPS3L',
          anonymizeIP: false,
        },
      }),
    ],
  ],
  plugins: [
    ...SECTIONS,
    [
      '@docusaurus/plugin-ideal-image',
      {
        quality: 80,
        max: 1030, // max resized image's size.
        min: 640, // min resized image's size. if original is lower, use that size.
        steps: 2, // the max number of images generated between min and max (inclusive)
        disableInDev: false,
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Evmos Docs',
        logo: {
          href: '/',
          alt: 'Evmos Logo',
          src: 'img/evmos.svg',
        },
        items: [
          {
            position: 'left',
            label: 'Use',
            to: '/use',
          },
          {
            position: 'left',
            label: 'Develop',
            to: '/develop',
          },
          {
            position: 'left',
            label: 'Validate',
            to: '/validate',
          },
          {
            position: 'left',
            label: 'Protocol',
            to: '/protocol',
          },
          {
            position: 'right',
            label: 'Tools',
            to: '/develop/tools',
          },          
          {
            position: 'right',
            label: 'Networks',
            to: '/develop/api/networks',
          },
          {
            position: 'right',
            label: 'App',
            to: 'https://app.evmos.org',
          },
          {
            href: 'https://github.com/evmos',
            className: 'pseudo-icon github-icon',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Use Evmos',
                to: '/use',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Telegram',
                href: 'https://t.me/EvmosOrg',
              },
              {
                label: 'Discord',
                href: 'https://discord.gg/evmos',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/EvmosOrg',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: 'https://medium.com/evmos',
              },
              {
                label: 'Evmos GitHub',
                href: 'https://github.com/evmos',
              },
            ],
          },
        ],
        copyright: `Built with ❤️ by the Evmos Core Development Team. © ${new Date().getFullYear()} All rights reserved.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
