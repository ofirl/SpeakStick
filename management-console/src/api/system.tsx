import { UseQueryOptions, useMutation, useQuery } from "@tanstack/react-query";
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

export type NetowrkScanResult = { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string };
export const useScanNetworks = (options: UseQueryOptions<NetowrkScanResult[], unknown, NetowrkScanResult[], string[]> = {}) => {
    return useQuery(
        ['network', 'scan'],
        () => axios.get(baseUrl + "/network/scan").then(value => value.data as { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string }[]),
        options
    )
};

type NetworkConfiguration = {
    ssid: string,
    psk?: string,
    key_mgmt: string
}
export const useUpdateNetworkConfiguration = () => {
    return useMutation(({ ssid, psk, key_mgmt }: NetworkConfiguration) =>
        axios.post(baseUrl + "/network/update", {
            ssid, psk, key_mgmt
        }).then(value => value.status === 200),
        {
            onSuccess: () => {
                toast.success("Network configuration updated")
            }
        }
    )
};