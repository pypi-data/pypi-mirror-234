import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '51a'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', 'a50'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'b6b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'bf2'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', 'f2e'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', 'dc5'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', '9a0'),
    exact: true
  },
  {
    path: '/blog/2016/03/11/blog-post',
    component: ComponentCreator('/blog/2016/03/11/blog-post', 'b94'),
    exact: true
  },
  {
    path: '/blog/2017/04/10/blog-post-two',
    component: ComponentCreator('/blog/2017/04/10/blog-post-two', 'd8b'),
    exact: true
  },
  {
    path: '/blog/2017/09/25/testing-rss',
    component: ComponentCreator('/blog/2017/09/25/testing-rss', '8f1'),
    exact: true
  },
  {
    path: '/blog/2017/09/26/adding-rss',
    component: ComponentCreator('/blog/2017/09/26/adding-rss', 'ac2'),
    exact: true
  },
  {
    path: '/blog/2017/10/24/new-version-1.0.0',
    component: ComponentCreator('/blog/2017/10/24/new-version-1.0.0', '5a3'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '4bd'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'afe'),
    routes: [
      {
        path: '/docs/sdk-reference/soil/alerts/',
        component: ComponentCreator('/docs/sdk-reference/soil/alerts/', 'c4a'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/alias',
        component: ComponentCreator('/docs/sdk-reference/soil/alias', 'a65'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/api',
        component: ComponentCreator('/docs/sdk-reference/soil/api', '801'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/configuration',
        component: ComponentCreator('/docs/sdk-reference/soil/configuration', '52d'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/connectors/elastic_search',
        component: ComponentCreator('/docs/sdk-reference/soil/connectors/elastic_search', '6ef'),
        exact: true
      },
      {
        path: '/docs/sdk-reference/soil/data',
        component: ComponentCreator('/docs/sdk-reference/soil/data', '36d'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/data_structure',
        component: ComponentCreator('/docs/sdk-reference/soil/data_structure', 'bce'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/decorator',
        component: ComponentCreator('/docs/sdk-reference/soil/decorator', '616'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/dictionary',
        component: ComponentCreator('/docs/sdk-reference/soil/dictionary', '9df'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/errors',
        component: ComponentCreator('/docs/sdk-reference/soil/errors', '9db'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/finder',
        component: ComponentCreator('/docs/sdk-reference/soil/finder', 'd5d'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/modulify',
        component: ComponentCreator('/docs/sdk-reference/soil/modulify', 'a6f'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/pipeline',
        component: ComponentCreator('/docs/sdk-reference/soil/pipeline', '9d9'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/storage/base_storage',
        component: ComponentCreator('/docs/sdk-reference/soil/storage/base_storage', '310'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/storage/compound_storage',
        component: ComponentCreator('/docs/sdk-reference/soil/storage/compound_storage', '96c'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/storage/elasticsearch',
        component: ComponentCreator('/docs/sdk-reference/soil/storage/elasticsearch', '02b'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/storage/object_storage',
        component: ComponentCreator('/docs/sdk-reference/soil/storage/object_storage', '613'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/task',
        component: ComponentCreator('/docs/sdk-reference/soil/task', '940'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/types',
        component: ComponentCreator('/docs/sdk-reference/soil/types', 'e80'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/sdk-reference/soil/utils',
        component: ComponentCreator('/docs/sdk-reference/soil/utils', '179'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/data_structure',
        component: ComponentCreator('/docs/soil-library/data_structures/data_structure', '420'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/frequent_itemsets',
        component: ComponentCreator('/docs/soil-library/data_structures/frequent_itemsets', 'ac5'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/hypergraph',
        component: ComponentCreator('/docs/soil-library/data_structures/hypergraph', 'b81'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/NBClusters',
        component: ComponentCreator('/docs/soil-library/data_structures/NBClusters', '02a'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/predefined/dict',
        component: ComponentCreator('/docs/soil-library/data_structures/predefined/dict', 'c54'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/predefined/list',
        component: ComponentCreator('/docs/soil-library/data_structures/predefined/list', '1a6'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/predefined/ndarray',
        component: ComponentCreator('/docs/soil-library/data_structures/predefined/ndarray', '667'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/predefined/object_ds',
        component: ComponentCreator('/docs/soil-library/data_structures/predefined/object_ds', 'bd0'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/predefined/pd_data_frame',
        component: ComponentCreator('/docs/soil-library/data_structures/predefined/pd_data_frame', '162'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/streams/patients',
        component: ComponentCreator('/docs/soil-library/data_structures/streams/patients', 'd03'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/streams/stream',
        component: ComponentCreator('/docs/soil-library/data_structures/streams/stream', 'bad'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/data_structures/streams/trajectory_clusters',
        component: ComponentCreator('/docs/soil-library/data_structures/streams/trajectory_clusters', '5fd'),
        exact: true
      },
      {
        path: '/docs/soil-library/modules/clustering/NBClustering',
        component: ComponentCreator('/docs/soil-library/modules/clustering/NBClustering', '3d1'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/clustering/NBClustering_categorical',
        component: ComponentCreator('/docs/soil-library/modules/clustering/NBClustering_categorical', 'f10'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/clustering/SIDIWO/',
        component: ComponentCreator('/docs/soil-library/modules/clustering/SIDIWO/', 'efe'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/experiment',
        component: ComponentCreator('/docs/soil-library/modules/experiment', 'b9a'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/higher_order/Predictor',
        component: ComponentCreator('/docs/soil-library/modules/higher_order/Predictor', '0fc'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/itemsets/frequent_itemsets_compare',
        component: ComponentCreator('/docs/soil-library/modules/itemsets/frequent_itemsets_compare', 'b7a'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/itemsets/frequent_itemsets_hypergraph',
        component: ComponentCreator('/docs/soil-library/modules/itemsets/frequent_itemsets_hypergraph', 'a3b'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/preprocessing/filters/events_filter',
        component: ComponentCreator('/docs/soil-library/modules/preprocessing/filters/events_filter', '208'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/preprocessing/filters/row_filter',
        component: ComponentCreator('/docs/soil-library/modules/preprocessing/filters/row_filter', '52d'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/statistics/customstatistics',
        component: ComponentCreator('/docs/soil-library/modules/statistics/customstatistics', '7dc'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/statistics/time_statistics',
        component: ComponentCreator('/docs/soil-library/modules/statistics/time_statistics', '690'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/soil-library/modules/temporal/trajectories',
        component: ComponentCreator('/docs/soil-library/modules/temporal/trajectories', 'fb3'),
        exact: true
      },
      {
        path: '/docs/tutorial/alerts',
        component: ComponentCreator('/docs/tutorial/alerts', '8e4'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/data',
        component: ComponentCreator('/docs/tutorial/data', '110'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/data-structures',
        component: ComponentCreator('/docs/tutorial/data-structures', '90a'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/deployments',
        component: ComponentCreator('/docs/tutorial/deployments', '58b'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/get-started',
        component: ComponentCreator('/docs/tutorial/get-started', '57e'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/logging',
        component: ComponentCreator('/docs/tutorial/logging', 'fff'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/modules',
        component: ComponentCreator('/docs/tutorial/modules', 'd32'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/notebooks',
        component: ComponentCreator('/docs/tutorial/notebooks', '186'),
        exact: true,
        sidebar: "docs"
      },
      {
        path: '/docs/tutorial/scripts',
        component: ComponentCreator('/docs/tutorial/scripts', '1a0'),
        exact: true,
        sidebar: "docs"
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'f3d'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
