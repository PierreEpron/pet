import axios from 'axios';

const REACT_APP_API_URL = "http://localhost:8000/api"
const HOME_URL = "/HomePage"

function login(user, msgHandler) {
    axios.post(REACT_APP_API_URL + "/token/", JSON.stringify(user), {headers: {"Content-Type":"application/json"}})
        .then(function (response) {
            if (response.status === 200 ) {
                localStorage.setItem('currentUser', JSON.stringify({
                    userName:user.username,
                    access:response.data.access,
                    refresh:response.data.refresh
                }));    
                window.location = HOME_URL
            }
        })
        .catch(function (error) {
            console.log(error.response.status)
            switch (error.response.status) {
                case 400:
                    msgHandler('Email and Password should not be blank.')
                    break
                case 401:
                    msgHandler('Bad Email or Password.')
                    break
                default:
                    console.log(error)
                    break
            }
        })
}

function logout() {
    console.log("logout")
    localStorage.removeItem('currentUser');
}


export {login, logout}