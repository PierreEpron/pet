import axios from 'axios';

const REACT_APP_API_URL = "http://localhost:8000/api"

function login(user) {
    axios.post(REACT_APP_API_URL + "/token/", JSON.stringify(user), {headers: {"Content-Type":"application/json"}})
        .then(function (response) {
            if (response.status === 200 ) {
                localStorage.setItem('currentUser', JSON.stringify({
                    userName:user.username,
                    access:response.data.access,
                    refresh:response.data.refresh
                }));
                window.location = "/HomePage"
            }
        })
        .catch(function (error) {
            if (response.status === 401 ) {

            }
            else {
                console.log(error);
            }
        })
}

function logout() {
    console.log("logout")
    localStorage.removeItem('currentUser');
}


export {login, logout}