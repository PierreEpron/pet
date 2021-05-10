import React from 'react';
import SignIn from "./components/SignIn";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Pages1 from "./pages/Pages1"

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/" exact component={() => <SignIn />} />
            <Route path="/pages1" exact component={() => <Pages1 />} />
            {/*<Route path="/pagestest" exact component={() => <PageTest />} />*/}
        </Switch>
      </Router>

    </div>
  );
}


export default App;
