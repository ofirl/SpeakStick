import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useRestartStickController = () => {
    return useMutation(() =>
        axios.get(baseUrl + "/restart/stick-controller").then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Stick controller restarted")
            },
            onError: () => {
                toast.error("Error restarting stick controller")
            }
        }
    )
};

export const useUpgradeApplication = () => {
    return useMutation(() =>
        axios.get(baseUrl + "/upgrade").then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Application is upgrading, this might take a few minutes")
            },
            onError: () => {
                toast.error("Error starting application upgrade")
            }
        }
    )
};