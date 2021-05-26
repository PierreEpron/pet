import axios from 'axios';
import {REACT_APP_API_URL, SIGNIN_URL} from './apiConfig'
import {getHeader, clearCurrentUser, parseQuery} from './apiHelpers'

function getContents(path, query, dataHandler) {
    axios.get(REACT_APP_API_URL + path + '?' + parseQuery(query), {headers: getHeader(true)})
        .then(function (response) {
            console.log(response)
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