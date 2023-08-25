import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const baseUrl = "http://speakstick.local"

export const useGetConfigs = () => {
    return useQuery(['configs'], () => axios.get(baseUrl + "/api/configs"))
};