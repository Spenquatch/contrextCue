/* tslint:disable */
/* eslint-disable */
/**
 * ContrextCue Sidecar API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import type { Configuration } from '../configuration';
import type { AxiosPromise, AxiosInstance, RawAxiosRequestConfig } from 'axios';
import globalAxios from 'axios';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from '../common';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, type RequestArgs, BaseAPI, RequiredError, operationServerMap } from '../base';
// @ts-ignore
import type { StatusResponse } from '../models';
/**
 * StatusApi - axios parameter creator
 * @export
 */
export const StatusApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Retrieves the current status of system components and configuration.                        Returns information about:            - LLM status (model name and whether it\'s loaded successfully)            - Speech-to-text engine status (engine name and model)            - Current keyboard shortcut configuration            - Warm-up status for performance optimization                        This endpoint is used by the UI to display system status and verify that components are functioning.
         * @summary Get system health and configuration status
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getStatusApiV1StatusGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/status/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * StatusApi - functional programming interface
 * @export
 */
export const StatusApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = StatusApiAxiosParamCreator(configuration)
    return {
        /**
         * Retrieves the current status of system components and configuration.                        Returns information about:            - LLM status (model name and whether it\'s loaded successfully)            - Speech-to-text engine status (engine name and model)            - Current keyboard shortcut configuration            - Warm-up status for performance optimization                        This endpoint is used by the UI to display system status and verify that components are functioning.
         * @summary Get system health and configuration status
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getStatusApiV1StatusGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<StatusResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getStatusApiV1StatusGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['StatusApi.getStatusApiV1StatusGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
    }
};

/**
 * StatusApi - factory interface
 * @export
 */
export const StatusApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = StatusApiFp(configuration)
    return {
        /**
         * Retrieves the current status of system components and configuration.                        Returns information about:            - LLM status (model name and whether it\'s loaded successfully)            - Speech-to-text engine status (engine name and model)            - Current keyboard shortcut configuration            - Warm-up status for performance optimization                        This endpoint is used by the UI to display system status and verify that components are functioning.
         * @summary Get system health and configuration status
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getStatusApiV1StatusGet(options?: RawAxiosRequestConfig): AxiosPromise<StatusResponse> {
            return localVarFp.getStatusApiV1StatusGet(options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * StatusApi - object-oriented interface
 * @export
 * @class StatusApi
 * @extends {BaseAPI}
 */
export class StatusApi extends BaseAPI {
    /**
     * Retrieves the current status of system components and configuration.                        Returns information about:            - LLM status (model name and whether it\'s loaded successfully)            - Speech-to-text engine status (engine name and model)            - Current keyboard shortcut configuration            - Warm-up status for performance optimization                        This endpoint is used by the UI to display system status and verify that components are functioning.
     * @summary Get system health and configuration status
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof StatusApi
     */
    public getStatusApiV1StatusGet(options?: RawAxiosRequestConfig) {
        return StatusApiFp(this.configuration).getStatusApiV1StatusGet(options).then((request) => request(this.axios, this.basePath));
    }
}

