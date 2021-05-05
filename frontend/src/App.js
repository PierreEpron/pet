import React from 'react';
import Header from "./components/Header";
import SignIn from "./components/SignIn";
 // eslint-disable-next-line
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
 // eslint-disable-next-line
import ExportButton from "./components/ExportButton";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/" exact component={() => <SignIn />} />
          <Route path="/header" exact component={() => <Header />} />

        </Switch>
      </Router>
    </div>
  );
}


export default App;
