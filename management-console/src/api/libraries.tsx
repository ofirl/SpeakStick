import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

// import { toast } from "react-toastify";

type Library = {
    id: number,
    name: string,
    description: string,
    active: boolean,
    editable: boolean
}

export const useGetLibraries = () => {
    return useQuery(['libraries'], () => axios.get(`${baseUrl}/libraries`).then(value => value.data as Library[]))
};