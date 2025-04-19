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


// May contain unused imports in some cases
// @ts-ignore
import type { Mode } from './mode';

/**
 * 
 * @export
 * @interface RewriteRequest
 */
export interface RewriteRequest {
    /**
     * The user-defined trigger name (e.g., \'rewrite\', \'email\') that activated this request
     * @type {string}
     * @memberof RewriteRequest
     */
    'trigger': string;
    /**
     * The prompt template to apply to the input text before sending to the LLM
     * @type {string}
     * @memberof RewriteRequest
     */
    'prompt': string;
    /**
     * The raw text input that needs to be processed by the LLM
     * @type {string}
     * @memberof RewriteRequest
     */
    'input': string;
    /**
     * The insertion mode determining how output text should be placed (\'append\' or \'replace\')
     * @type {Mode}
     * @memberof RewriteRequest
     */
    'mode': Mode;
    /**
     * Whether to copy the result to the clipboard
     * @type {boolean}
     * @memberof RewriteRequest
     */
    'clipboard'?: boolean;
    /**
     * Whether to automatically paste the result at the cursor position
     * @type {boolean}
     * @memberof RewriteRequest
     */
    'autoPaste'?: boolean;
}



