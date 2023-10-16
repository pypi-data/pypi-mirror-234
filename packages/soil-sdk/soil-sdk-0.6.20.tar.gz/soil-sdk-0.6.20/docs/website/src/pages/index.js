import React from 'react'
import Layout from "@theme/Layout"
import Button from '@material-ui/core/Button'
import makeStyles from '@material-ui/core/styles/makeStyles'
import Grid from '@material-ui/core/Grid'
import { useColorMode } from '@docusaurus/theme-common'
import useBaseUrl from '@docusaurus/useBaseUrl'
import Typography from '@material-ui/core/Typography'
import Highlight, { defaultProps, } from "prism-react-renderer";
import codeTheme from 'prism-react-renderer/themes/vsDark';

import {
  createMuiTheme,
  ThemeProvider,
} from '@material-ui/core/styles'

const generateTheme = (darkMode) => createMuiTheme({
  palette: {
    type: darkMode ? 'dark' : 'light',
    primary: {
      main: '#558b2f'
    }
  }
});

const useStyles = makeStyles(theme => {
  return {
    root: {
      padding: theme.spacing(2)
    },
    mainTitle: {
      fontWeight: 'bold'
    },
    mainElement: {
      textAlign: 'center'
    },
    hero: {
      margin: theme.spacing(2),
      maxWidth: '30%',
      textAlign: 'center'
    },
    heroImageContainer: {
      maxWidth: '30%'
    },
    heroTitle: {
      fontWeight: 'bolder'
    }
  }
})

const exampleCode = `
import soil
from soil.modules.preprocessing.filters import row_filter
from soil.modules.simple_module import my_module
patients = soil.data('my_data')
women, = row_filter.RowFilter(patients, sex={'eql': '1'})
statistics, = my_module(women, aggregation_column='age')
print(statistics.data)
`;

const Hero = ({ title, text, imgPath }) => {
  const classes = useStyles()
  return (
    <Grid item container className={classes.hero} justify="center" alignItems="center" direction="column">
      <Grid item className={classes.heroImageContainer} justify="center" alignItems="center">
        <img alt="example-app" src={useBaseUrl(imgPath)} />
      </Grid>
      <Grid item justify="center" alignItems="center">
        <Typography variant="h5" gutterBottom className={classes.heroTitle}>
          {title}
        </Typography>
        <Typography>
          {text}
        </Typography>
      </Grid>

    </Grid>
  )
}

const App = ({ config }) => {
  const { colorMode } = useColorMode()
  const theme = React.useMemo(() => generateTheme(colorMode), [colorMode])
  const classes = useStyles()
  console.log(config)
  return (
    <ThemeProvider theme={theme}>
      <Grid container className={classes.root} justify="center" alignItems="center">
        <Grid item className={classes.mainElement} >
          <Typography variant="h3" color="primary" gutterBottom className={classes.mainTitle}>{config.title}</Typography>
          <Typography variant="h4" color="primary" gutterBottom>{config.tagline}</Typography>
          <Button variant="outlined" color="primary" size="large" href="docs/tutorial/get-started">Get Started</Button>
        </Grid>
      </Grid>
      <Grid container className={classes.root} justify="center" alignItems="center">
        <Hero
          title="Write the code once"
          text="Prototype, develop, test and deploy with the same tool"
          imgPath="img/undraw_operating_system.svg"
        />
        <Hero
          title="Parallelize the code automatically"
          text="Don't worry about pipelines"
          imgPath="img/undraw_version_control_9bpv.svg"
        />
        <Hero
          title="Don't reinvent the wheel"
          text="You can use the SOIL Library for typical modules such as filtering, clustering, basic statistics, ..."
          imgPath="img/undraw_abstract_x68e.svg"
        />
      </Grid>
      <Grid container className={classes.root} justify="center" alignItems="center" direction="row" style={{ backgroundColor: colorMode ? '#444444' : '#f7f7f7' }}>
        <Grid item xs={4}>
          <Typography variant="h5" style={{ fontWeight: 'bolder' }} gutterBottom>
            Run cloud and local modules seemingly
          </Typography>
          <Highlight {...defaultProps} code={exampleCode} language="python" theme={codeTheme}>
            {({ className, style, tokens, getLineProps, getTokenProps }) => (
              <pre className={className} style={style}>
                {tokens.map((line, i) => (
                  <div {...getLineProps({ line, key: i })}>
                    {line.map((token, key) => (
                      <span {...getTokenProps({ token, key })} />
                    ))}
                  </div>
                ))}
              </pre>
            )}
          </Highlight>
        </Grid>
        <Grid item xs={2}>
          <img src={useBaseUrl('img/undraw_server_push_vtms.svg')} />
        </Grid>
      </Grid>

    </ThemeProvider>
  );
};


const Index = (props) => {
  return (
    <Layout>
      <App {...props} />
    </Layout>
  )
}
export default Index
