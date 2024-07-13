import {
    ADMIN_LOGIN_REQUEST,
        ADMIN_LOGIN_SUCCESS,
        ADMIN_LOGIN_FAIL,
        ADMIN_LOGOUT,
}
from '../constants/adminConstants'
import axios from 'axios';

export const login = (email, password) => async(dispatch) =>{
    try{
        dispatch({
            type:ADMIN_LOGIN_REQUEST
        } )

        const config = {
            headers: {
                'content-type': 'application/json'
            }
        }

        const {data} = await axios.post(
            '/api/users/login/',
            {'username': email, 'password': password},
            config
        )

        dispatch({
            type: ADMIN_LOGIN_SUCCESS,
            payload: data
        })

        localStorage.setItem('userInfo', JSON.stringify(data))
    }catch(error){
        dispatch({
            type: ADMIN_LOGIN_FAIL,
            payload:error.response  && error.response.data.detail 
            ? error.response.data.detail 
            : error.message
         })
    }

}


export const logout = () => (dispatch) => {
    localStorage.removeItem('userInfo') 
    dispatch( {type : ADMIN_LOGOUT})
} 