import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

export const useRestartStickController = () => {
    return useMutation(() =>
        axios.get(baseUrl + "/api/restart/stick-controller").then(value => value.status === 200),
    )
};