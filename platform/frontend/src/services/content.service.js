import axios from 'axios';
import {REACT_APP_API_URL, SIGNIN_URL, get_header, clearCurrentUser} from './apiConfig'


function parse_query(query) {
    const parsed = []
    for (var key in query)
        parsed.push(encodeURIComponent(key) + '=' + encodeURIComponent(query[key]))
    return parsed.join('&')
}

function get_contents(path, query, dataHandler) {
    console.log(get_header(true))
    axios.get(REACT_APP_API_URL + path + '?' + query, {headers: get_header(true)})
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
    return parse_query(query)
}

export {get_contents}