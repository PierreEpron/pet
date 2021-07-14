import axios from 'axios';
import {onBadAuth} from './auth.service'
import {REACT_APP_API_URL} from './apiConfig'
import {getHeader, parseQuery} from './apiHelpers'

const errorHandler = (error) => {
    switch (error.response.status) {
        case 401:
            onBadAuth()
            break
        default:
            console.log(error)
            break             
    }   
}

function getContents(path, query, successHandler) {
    axios.get(REACT_APP_API_URL + path + '?' + parseQuery(query), {headers: getHeader(true)})
        .then(function (response) {
            successHandler(response.data);
        })
        .catch(errorHandler);
}

function putContent(path, data, successHandler, data_to_json=true) {
    const parsed = data_to_json ? JSON.stringify(data) : data;
    axios.patch(REACT_APP_API_URL + path, parsed,  {headers: getHeader(true)})
        .then((response) => {
            successHandler(response.data);
        })
        .catch(errorHandler);
}

function postContent(path, data, successHandler, data_to_json=true) {
    const parsed = data_to_json ? JSON.stringify(data) : data;
    axios.post(REACT_APP_API_URL + path, parsed,  {headers: getHeader(true)})
        .then((response) => {
            successHandler(response.data);
        })
        .catch(errorHandler);
}

function deleteContent(path, successHandler) {
    axios.delete(REACT_APP_API_URL + path, {headers:getHeader(true)})
        .then((response) => {
            successHandler(response.data);
        })
        .catch(errorHandler);
}

export {getContents, putContent, postContent, deleteContent}