import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export const useGetConfigs = () => {
    return useQuery(['configs'], () => axios.get("/api/configs"))
};