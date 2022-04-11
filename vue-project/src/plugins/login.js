import axios from "axios";
import Cookies from "js-cookie";

export async function Login() {
  try {
    const token = await axios.post("http://localhost:8000/auth");
    Cookies.set("access_token", token.data.data.access_token, "15m");
    Cookies.set("refresh_token", token.data.data.refresh_token, "30d");

    axios.defaults.headers["refresh_token"] = Cookies.get("refresh_token");

    return token;
  } catch (err) {
    return err;
  }
}

export async function refreshToken() {
  try {
    const token = await axios.post("http://localhost:8000/auth");
    Cookies.set("token", token.data.data.token, "15m");
    return token;
  } catch (err) {
    return err;
  }
}
