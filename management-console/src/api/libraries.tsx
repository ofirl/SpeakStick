import { UseQueryOptions, useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

// import { toast } from "react-toastify";

export type Library = {
    id: number,
    name: string,
    description: string,
    active: boolean,
    editable: boolean
}

export const useGetLibraries = (options: UseQueryOptions<Library[], unknown, Library[], string[]> = {}) => {
    return useQuery(['libraries'], () => axios.get(`${baseUrl}/libraries`).then(value => value.data as Library[]), options)
};