import axios from 'axios';
import {onBadAuth} from './auth.service'
import {REACT_APP_API_URL} from './apiConfig'
import {getHeader, parseQuery} from './apiHelpers'

function getContents(path, query, dataHandler) {
    axios.get(REACT_APP_API_URL + path + '?' + parseQuery(query), {headers: getHeader(true)})
        .then(function (response) {
            dataHandler(response.data)
        })
        .catch(function (error) {
            switch (error.response.status) {
                case 401:
                    onBadAuth()
                    break
                default:
                    console.log(error)
                    break             
            }        
        })
}

function putContent(path, data, successHandler) {
    axios.patch(REACT_APP_API_URL + path + '/', JSON.stringify(data),  {headers: getHeader(true)})
        .then((response) => {
            successHandler(response)
        })
        .catch((error) => {
            switch (error.response.status) {
                case 401:
                    onBadAuth()
                    break
                default:
                    console.log(error)
                    break               
            }        
        })  
}

export {getContents, putContent}