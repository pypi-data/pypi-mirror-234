/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */


// Workaround service that allows for the modal launchContext object to be used
// in any controller/service.
(function () {
    'use strict';
    angular
        .module('gbpui.group-member')
        .factory('gbpui.group-member.launch-context.service', launchContextService);


    launchContextService.$inject = [
        '$location',
        'horizon.framework.util.http.service',
    ];

    function launchContextService($location,apiService) {
        var policyGroups = {'data':[],'status':0};                                                                                                                                       
        !$location.absUrl().includes('login') && apiService
            .get('project/policytargets/policy_target_groups')
            .error(function () {  
                policyGroups.status = 1   
            }).then(data => { 
                policyGroups.data = data.data;  
                policyGroups.status = 1;
            });
        return {
            launchContext: {
                defaults: [],
                policyGroups,
            }
        };
    }
})();