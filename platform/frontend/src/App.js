import React, { useState } from 'react';
import SignIn from "./components/SignIn";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import HomePage from './pages/HomePage'
import Docpage from "./pages/DocPage"
import StatPage from "./pages/StatPage"
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import deepPurple from '@material-ui/core/colors/deepPurple';


function App() {
    const prefersDarkMode = useMediaQuery('(prefers-color-scheme: light)');
    const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'light' : 'dark',
            primary: deepPurple,
            secondary: deepPurple,
        },
      }),
    [prefersDarkMode],
    );



    return (
        <div className="App">
            <ThemeProvider theme={theme}>
            <CssBaseline/>

            <Router>
                <Switch>

                    <Route path="/" exact component={SignIn}/>
                    <Route path="/HomePage" exact component={HomePage}/>
                    <Route path="/document/:id" exact component={Docpage}/>
                    <Route path="/StatPage" exact component={StatPage}/>

                </Switch>
            </Router>
            </ThemeProvider>

        </div>
    );
}


export default App;
