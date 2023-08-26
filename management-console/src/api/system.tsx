import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useRestartStickController = () => {
    return useMutation(() =>
        axios.get(baseUrl + "/api/restart/stick-controller").then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Stick controller restarted")
            }
        }
    )
};