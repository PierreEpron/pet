import axios from 'axios';
import {REACT_APP_API_URL, HOME_URL, SIGNIN_URL} from './apiConfig'
import {getHeader, clearCurrentUser} from './apiHelpers'

function login(user, msgHandler) {
    axios.post(REACT_APP_API_URL + "/token/", JSON.stringify(user), {headers: getHeader(false)})
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

function onBadAuth() {
    const user = JSON.parse(localStorage.getItem("currentUser"))
    if (user)
        axios.post(REACT_APP_API_URL + "/token/refresh/", JSON.stringify({refresh:user.refresh}), {headers: getHeader(false)})
            .then(function (response) {
                localStorage.setItem('currentUser', JSON.stringify({
                    userName:user.username,
                    access:response.data.access,
                    refresh:user.refresh
                }));    
                window.location = HOME_URL
            })
            .catch(function (error) {
                clearCurrentUser()
                window.location = SIGNIN_URL  
            })
    else         
        window.location = SIGNIN_URL  
}


function logout() {
    console.log("logout")
    localStorage.removeItem('currentUser');
}


export {login, logout, onBadAuth}