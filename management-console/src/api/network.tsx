import { UseQueryOptions, useMutation, useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";
import { toast } from "react-toastify";

export type NetworkStatusResult = { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string };
export const useGetNetworkStatus = (options: UseQueryOptions<NetworkStatusResult, unknown, NetworkStatusResult, string[]> = {}) => {
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
        axios.post(baseUrl + "/network", {
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