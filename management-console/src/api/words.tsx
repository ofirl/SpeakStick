import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

// import { toast } from "react-toastify";

export const useGetWords = () => {
    return useQuery(['words'], () => axios.get(baseUrl + "/api/words").then(value => value.data as string[]))
};