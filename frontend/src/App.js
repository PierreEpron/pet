import React from 'react';
import Header from "./components/Header";
import SignIn from "./components/SignIn";
 // eslint-disable-next-line
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
 // eslint-disable-next-line
import ExportButton from "./components/ExportButton";
import Pages1 from "./pages/Pages1"

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/" exact component={() => <SignIn />} />
          <Route path="/pages1" exact component={() => <Pages1 />} />

        </Switch>
      </Router>
    </div>
  );
}


export default App;
