import axios from 'axios';
import {REACT_APP_API_URL, HOME_URL, get_header} from './apiConfig'



function login(user, msgHandler) {
    axios.post(REACT_APP_API_URL + "/token/", JSON.stringify(user), {headers: get_header(false)})
        .then(function (response) {
            localStorage.setItem('currentUser', JSON.stringify({
                userName:user.username,
                access:response.data.access,
                refresh:response.data.refresh
            }));    
            window.location = HOME_URL
        })
        .catch(function (error) {
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