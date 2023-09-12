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

export type NetworkStatusResult = { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string };
export const useGetNetworkStatus = (options: UseQueryOptions<NetworkStatusResult, unknown, NetworkStatusResult, string[]>) => {
    return useQuery(
        ['network', 'status'],
        () => axios.get(baseUrl + "/network/status").then(value => value.data as NetworkStatusResult),
        {
            refetchInterval: 10000,
            ...options
        },
    )
};

export type NetowrkScanResult = { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string };
export const useScanNetworks = (options: UseQueryOptions<NetowrkScanResult[], unknown, NetowrkScanResult[], string[]> = {}) => {
    return useQuery(
        ['network', 'scan'],
        () => axios.get(baseUrl + "/network/scan").then(value => value.data as NetowrkScanResult[]),
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
            },
            onError: () => {
                toast.error("Error updating network configuration")
            }
        }
    )
};