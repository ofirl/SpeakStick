import { useMutation, useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useRestartStickController = () => {
    return useMutation(() =>
        axios.get(baseUrl + "/restart/stick-controller").then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Stick controller restarted")
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
            }
        }
    )
};

export const useGetNetworkStatus = () => {
    return useQuery(['network', 'status'], () => axios.get(baseUrl + "/network/status").then(value => value.data as { ssid: string, signal_strength: number }))
};

export const useScanNetworks = () => {
    return useQuery(['network', 'scan'], () => axios.get(baseUrl + "/network/scan").then(value => value.data as { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string }[]))
};