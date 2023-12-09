import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptionsShort, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

export type NetworkStatusResult = { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string };
export const useGetNetworkStatus = (options?: UseCreateQueryWrapperOptionsShort<NetworkStatusResult>) => {
  return useCreateQuery({
    queryKey: ['network', 'status'],
    queryFn: () => axiosClient.get("/network/status").then(value => value.data as NetworkStatusResult),
    refetchInterval: 10000,
    errorMsg: "Error getting network status",
    ...options
  })
};

export type NetowrkScanResult = { ssid: string, signal_strength: number, secured: boolean, key_mgmt: string };
export const useScanNetworks = (options: UseCreateQueryWrapperOptionsShort<NetowrkScanResult[]>) => {
  return useCreateQuery({
    queryKey: ['network', 'scan'],
    queryFn: () => axiosClient.get("/network/scan").then(value => value.data as NetowrkScanResult[]),
    errorMsg: "Error scanning fpr networks",
    ...options
  })
};

type NetworkConfiguration = {
  ssid: string,
  psk?: string,
  key_mgmt: string
}
export const useUpdateNetworkConfiguration = (options?: UseCreateMutationWrapperOptions<boolean, NetworkConfiguration>) => {
  return useCreateMutation({
    mutationFn: ({ ssid, psk, key_mgmt }: NetworkConfiguration) =>
      axiosClient.post("/network", {
        ssid, psk, key_mgmt
      }).then(value => value.status === 200),
    successMsg: "Network configuration updated",
    errorMsg: "Error updating network configuration",
    ...options
  })
};