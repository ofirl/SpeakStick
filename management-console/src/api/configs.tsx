import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

export const useGetConfigs = () => {
    return useQuery(['configs'], () => axios.get(baseUrl + "/api/configs").then(value => value.data as Record<string, string>))
};