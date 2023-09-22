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

export const useResetToFactorySettings = () => {
    return useMutation(() =>
        axios.get(baseUrl + "/reset_factory_settings").then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Application is resetting to factory settings, this might take a few seconds")
            },
            onError: () => {
                toast.error("Error resetting application to factory settings")
            }
        }
    )
};