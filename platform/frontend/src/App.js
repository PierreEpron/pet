import React from 'react';
import SignIn from "./components/SignIn";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import HomePage from './pages/HomePage'
import Docpage from "./pages/DocPage"
import StatPage from "./pages/StatPage"

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/" exact component={() => <SignIn />} />
            <Route path="/HomePage" exact component={() => <HomePage />} />
            <Route path="/Docpage" exact component={() => <Docpage />} />
            <Route path="/StatPage" exact component={() => <StatPage />} />
            {/*<Route path="/pagestest" exact component={() => <PageTest />} />*/}
        </Switch>
      </Router>

    </div>
  );
}


export default App;
