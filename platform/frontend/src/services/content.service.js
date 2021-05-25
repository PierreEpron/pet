import axios from 'axios';
import {REACT_APP_API_URL, SIGNIN_URL, getHeader, clearCurrentUser} from './apiConfig'

function parseQuery(query) {
    const parsed = []
    for (var key in query)
        parsed.push(encodeURIComponent(key) + '=' + encodeURIComponent(query[key]))
    return parsed.join('&')
}

function getContents(path, query, dataHandler) {
    axios.get(REACT_APP_API_URL + path + '?' + parseQuery(query), {headers: getHeader(true)})
        .then(function (response) {
            dataHandler(response.data)
        })
        .catch(function (error) {
            switch (error.response.status) {
                case 401:
                    clearCurrentUser()
                    window.location = SIGNIN_URL   
                    break
                default:
                    console.log(error)
                    break             
            }        
        })
}

export {getContents}