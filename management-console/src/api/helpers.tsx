import { QueryKey, UseMutationOptions, UseQueryOptions, useMutation, useQuery } from "@tanstack/react-query"
import axios from "axios"
import { baseUrl } from "./consts"

export const axiosClient = axios.create({
  baseURL: baseUrl
})

export type UseCreateQueryOptions<TQueryFnData, TData> = UseQueryOptions<TQueryFnData, Error, TData, QueryKey> & {
  errorMsg: string
}

export type UseCreateQueryWrapperOptions<TQueryFnData, TData> = Omit<UseCreateQueryOptions<TQueryFnData, TData>, "queryKey" | "errorMsg"> &
  Partial<Pick<UseCreateQueryOptions<TQueryFnData, TData>, "errorMsg">>
export type UseCreateQueryWrapperOptionsShort<TData> = UseCreateQueryWrapperOptions<TData, TData>

export const useCreateQuery = <TQueryFnData, TData>({ meta, errorMsg, ...options }: UseCreateQueryOptions<TQueryFnData, TData>) => {
  return useQuery({
    meta: {
      errorMsg,
      ...meta
    },
    ...options
  })
}

type UseCreateMutationOptions<TQueryFnData, TData> = UseMutationOptions<TQueryFnData, Error, TData, QueryKey> & {
  errorMsg: string,
  successMsg: string,
  invalidateQueries?: string[]
}

export type UseCreateMutationWrapperOptions<TQueryFnData, TData> = Omit<UseCreateMutationOptions<TQueryFnData, TData>, "queryKey" | "errorMsg" | "successMsg"> &
  Partial<Pick<UseCreateMutationOptions<TQueryFnData, TData>, "errorMsg" | "successMsg">>
export type UseCreateMutationWrapperOptionsShort<TData = unknown> = UseCreateMutationWrapperOptions<TData, TData>

export const useCreateMutation = <TQueryFnData, TData>({ meta, errorMsg, successMsg, invalidateQueries, ...options }: UseCreateMutationOptions<TQueryFnData, TData>) => {
  return useMutation({
    meta: {
      errorMsg,
      successMsg,
      invalidateQueries,
      ...meta
    },
    ...options
  })
}