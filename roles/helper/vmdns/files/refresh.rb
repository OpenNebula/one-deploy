#!/usr/bin/env ruby
# managed by one-deploy

def run(cmd)
    o = `#{cmd}`
    s = $?
    raise unless s.success?
    o
end

def debounce(lock_file = '/var/tmp/vmdns.lock')
    File.open(lock_file, File::CREAT | File::RDWR, 0o0644) do |lf|
        next unless lf.flock(File::LOCK_EX | File::LOCK_NB)
        begin
            # NOTE: This is not completely precise, but should be good enough
            #       for a simple reduction.
            sleep(1)
            yield
        ensure
            lf.flock(File::LOCK_UN)
        end
    end
end

def refresh(hosts_file = '/etc/hosts')
    File.open(hosts_file, File::RDONLY) do |hf|
        hf.each_line(chomp: true).each_with_object({block: false, lines: []}) do |line, acc|
            case line
            when '# BEGIN VMDNS (one-deploy)'
                acc[:block] = true
            when '# END VMDNS (one-deploy)'
                acc[:block] = false
            else
                acc[:lines] << line unless acc[:block]
            end
        end[:lines]
    end.then do |unmanaged|
        require 'json'

        document = JSON.parse run('onevm list --json')

        File.open(hosts_file, File::CREAT | File::TRUNC | File::WRONLY, 0o0644) do |hf|
            unmanaged.each do |line|
                hf.puts(line)
            end

            hf.puts('# BEGIN VMDNS (one-deploy)')

            document.dig('VM_POOL', 'VM')&.each do |vm|
                ip = [vm.dig('TEMPLATE', 'NIC')].flatten.dig(0, 'IP')
                next unless ip

                name = vm['NAME']
                next unless name

                id = vm['ID']
                next unless id

                hf.puts("#{ip} #{name} one-#{id}")
            end

            hf.puts('# END VMDNS (one-deploy)')
        end
    end
end

debounce { refresh }
