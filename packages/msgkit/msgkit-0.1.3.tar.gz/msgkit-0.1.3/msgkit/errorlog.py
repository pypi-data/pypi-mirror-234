class ErrorLog:

    def __init__(self):
        self.causenum = 0

    def printerror(self, num, msg):
        '''
        Prints the error number, message received, and potential causes and solutions if desired.
        The causes are printed out in decreasing order of likelihood.
        '''
        print(f'\nError received: {num}\n')
        print(f'Response from server: {msg}\n')
        print('Possible causes:')

        if str(num) == '404':
            causes = [
                'The URL was written incorrectly or typed into the browser incorrectly',
                'The resource was moved, deleted, or is expired',
                'The file may be in a different path/the path is typed in incorrectly',
                'The server may not have the necessary permissions to access the requested resource',
                'Misconfigured server settings, such as incorrect routing rules or missing configuration files',
                'If a web server is not configured to serve a default page (e.g., "index.html") and you don\'t specify a specific page in the URL',
                'Websites using content management systems (CMS) may generate 404 errors if the requested URL corresponds to a non-existent or unpublished page',
                'The website may be using URL rewriting to create user-friendly URLs (e.g., from /page?id=123 to /page/123)',
                'When working with APIs, there could be changes in the API\'s structure, endpoint names, or versioning',
                'Problems with DNS (Domain Name System) configuration',
                'In a network with load balancers or reverse proxies, misconfiguration can cause requests to be routed to non-existent endpoints',
            ]
            self.printCauses(causes)
            print('\nPossible solutions:')
            solutions = [
                'Check the URL or path',
                'Verify the resource exists',
                'Check the server logs',
                'Check permissions for the file or directory',
                'Check if cache and content management systems are interfering',
            ]
            self.printSolutions(solutions)

    def printCauses(self, causes):
        if self.causenum != 0:
            causes = causes[:self.causenum]
        for i, cause in enumerate(causes):
            print(f'{i + 1}.', cause)

    def printSolutions(self, solutions):
        for i, solution in enumerate(solutions):
            print(f'{i + 1}.', solution)