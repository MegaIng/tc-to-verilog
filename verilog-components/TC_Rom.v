module TC_Rom (clk, rst, load, save, address, in, out);
    parameter BIT_WIDTH = 16;
    parameter BIT_DEPTH = 256;
    //parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;

    reg [BIT_WIDTH-1:0] mem [0:BIT_DEPTH];
    
    integer fd;
    integer i;

    initial begin
        //hexfile <= HEX_FILE;
        i = ($value$plusargs(ARG_SIG, hexfile));
        $display("loading %0s", hexfile);
        fd = $fopen(hexfile, "r");
        if (fd) begin
            i = 0;
            while (i < BIT_DEPTH && !$feof(fd)) begin
                mem[i][7:0] = $fgetc(fd);
                if (BIT_WIDTH > 8 && !$feof(fd)) begin
                    mem[i][15:8] = $fgetc(fd);
                    if (BIT_WIDTH > 16 && !$feof(fd)) begin
                        mem[i][23:16] = $fgetc(fd);
                        if (!$feof(fd)) begin
                            mem[i][31:24] = $fgetc(fd);
                            if (BIT_WIDTH > 32 && !$feof(fd)) begin
                                mem[i][39:32] = $fgetc(fd);
                                if (!$feof(fd)) begin
                                    mem[i][47:40] = $fgetc(fd);
                                    if (!$feof(fd)) begin
                                        mem[i][55:48] = $fgetc(fd);
                                        if (!$feof(fd)) begin
                                            mem[i][63:56] = $fgetc(fd);
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
                i = i + 1;
            end
            $display("read %d bytes", i);
        end else begin
            $display("file not found");
        end
        $fclose(fd);
        out <= {BIT_WIDTH{1'b0}};
    end

    always @ (address or rst) begin
        if (load && !rst)
            out <= mem[address];
        else
            out <= {BIT_WIDTH{1'b0}};
    end
    always @ (negedge clk) begin
        if (save && !rst)
            mem[address] <= in;
    end
endmodule
